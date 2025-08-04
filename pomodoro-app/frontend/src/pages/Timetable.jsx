import React, { useState, useEffect } from 'react';
import { Plus, Calendar, Clock, Book, Coffee, Eye, Trash2 } from 'lucide-react';
import { api } from '../utils/api';

const Timetable = ({ user }) => {
  const [timetables, setTimetables] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedTimetable, setSelectedTimetable] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTimetables();
  }, []);

  const fetchTimetables = async () => {
    try {
      const response = await api.get('/timetables');
      setTimetables(response.data.timetables);
    } catch (error) {
      console.error('Failed to fetch timetables:', error);
    } finally {
      setLoading(false);
    }
  };

  const CreateTimetableForm = () => {
    const [formData, setFormData] = useState({
      title: '',
      description: '',
      date: new Date().toISOString().split('T')[0],
    });
    const [entries, setEntries] = useState([]);
    const [newEntry, setNewEntry] = useState({
      start_time: '',
      end_time: '',
      subject: '',
      is_break: false,
    });

    const handleAddEntry = () => {
      if (newEntry.start_time && newEntry.end_time && newEntry.subject) {
        setEntries([...entries, { ...newEntry }]);
        setNewEntry({
          start_time: '',
          end_time: '',
          subject: '',
          is_break: false,
        });
      }
    };

    const handleRemoveEntry = (index) => {
      setEntries(entries.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        await api.post('/timetables', {
          ...formData,
          entries: entries,
        });
        setShowCreateForm(false);
        fetchTimetables();
        setFormData({
          title: '',
          description: '',
          date: new Date().toISOString().split('T')[0],
        });
        setEntries([]);
      } catch (error) {
        console.error('Failed to create timetable:', error);
      }
    };

    return (
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
          Create New Timetable
        </h3>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Title
              </label>
              <input
                type="text"
                required
                className="input-field"
                placeholder="Study Schedule"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Date
              </label>
              <input
                type="date"
                required
                className="input-field"
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Description
            </label>
            <textarea
              className="input-field"
              rows="3"
              placeholder="Optional description..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          {/* Add Entry Section */}
          <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Add Time Slots
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
              <div>
                <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                  Start Time
                </label>
                <input
                  type="time"
                  className="input-field"
                  value={newEntry.start_time}
                  onChange={(e) => setNewEntry({ ...newEntry, start_time: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                  End Time
                </label>
                <input
                  type="time"
                  className="input-field"
                  value={newEntry.end_time}
                  onChange={(e) => setNewEntry({ ...newEntry, end_time: e.target.value })}
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                  Subject/Activity
                </label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="Mathematics, Break, etc."
                  value={newEntry.subject}
                  onChange={(e) => setNewEntry({ ...newEntry, subject: e.target.value })}
                />
              </div>
              <div className="flex items-end">
                <label className="flex items-center space-x-2 mb-2">
                  <input
                    type="checkbox"
                    className="rounded border-gray-300 text-primary-500 focus:ring-primary-500"
                    checked={newEntry.is_break}
                    onChange={(e) => setNewEntry({ ...newEntry, is_break: e.target.checked })}
                  />
                  <span className="text-xs text-gray-600 dark:text-gray-400">Break</span>
                </label>
              </div>
            </div>
            <button
              type="button"
              onClick={handleAddEntry}
              className="btn-secondary flex items-center space-x-2"
            >
              <Plus className="h-4 w-4" />
              <span>Add Entry</span>
            </button>
          </div>

          {/* Entries List */}
          {entries.length > 0 && (
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
                Schedule Preview
              </h4>
              <div className="space-y-2">
                {entries.map((entry, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
                  >
                    <div className="flex items-center space-x-4">
                      {entry.is_break ? (
                        <Coffee className="h-4 w-4 text-primary-500" />
                      ) : (
                        <Book className="h-4 w-4 text-primary-500" />
                      )}
                      <span className="font-medium text-gray-900 dark:text-white">
                        {entry.start_time} - {entry.end_time}
                      </span>
                      <span className="text-gray-600 dark:text-gray-400">
                        {entry.subject}
                      </span>
                      {entry.is_break && (
                        <span className="text-xs bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 px-2 py-1 rounded">
                          Break
                        </span>
                      )}
                    </div>
                    <button
                      type="button"
                      onClick={() => handleRemoveEntry(index)}
                      className="text-red-500 hover:text-red-700 p-1"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex space-x-4">
            <button type="submit" className="btn-primary">
              Create Timetable
            </button>
            <button
              type="button"
              onClick={() => setShowCreateForm(false)}
              className="btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  };

  const TimetableView = ({ timetable }) => {
    const [details, setDetails] = useState(null);
    const [loadingDetails, setLoadingDetails] = useState(true);

    useEffect(() => {
      if (timetable) {
        fetchTimetableDetails(timetable.id);
      }
    }, [timetable]);

    const fetchTimetableDetails = async (id) => {
      try {
        const response = await api.get(`/timetables/${id}`);
        setDetails(response.data);
      } catch (error) {
        console.error('Failed to fetch timetable details:', error);
      } finally {
        setLoadingDetails(false);
      }
    };

    if (loadingDetails) {
      return (
        <div className="card">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              {details.timetable.title}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              {new Date(details.timetable.date).toLocaleDateString()}
            </p>
            {details.timetable.description && (
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                {details.timetable.description}
              </p>
            )}
          </div>
          <button
            onClick={() => setSelectedTimetable(null)}
            className="btn-secondary"
          >
            Back to List
          </button>
        </div>

        <div className="space-y-3">
          {details.entries.map((entry, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border-l-4 ${
                entry.is_break
                  ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                  : 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {entry.is_break ? (
                    <Coffee className="h-5 w-5 text-green-500" />
                  ) : (
                    <Book className="h-5 w-5 text-primary-500" />
                  )}
                  <div>
                    <div className="font-medium text-gray-900 dark:text-white">
                      {entry.subject}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {entry.start_time} - {entry.end_time}
                    </div>
                  </div>
                </div>
                {entry.is_break && (
                  <span className="text-xs bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 px-2 py-1 rounded">
                    Break
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="card">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
                <div className="space-y-2">
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (selectedTimetable) {
    return <TimetableView timetable={selectedTimetable} />;
  }

  if (showCreateForm) {
    return <CreateTimetableForm />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Study Timetables
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Plan your study sessions and manage your schedule effectively
          </p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="h-5 w-5" />
          <span>Create Timetable</span>
        </button>
      </div>

      {timetables.length === 0 ? (
        <div className="card text-center py-12">
          <Calendar className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No timetables yet
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Create your first study timetable to get organized and boost your productivity.
          </p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="btn-primary"
          >
            Create Your First Timetable
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {timetables.map((timetable) => (
            <div key={timetable.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <Calendar className="h-6 w-6 text-primary-500" />
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {timetable.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {new Date(timetable.date).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
              
              {timetable.description && (
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
                  {timetable.description}
                </p>
              )}
              
              <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                <span className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>{timetable.entry_count} entries</span>
                </span>
                <span>
                  {new Date(timetable.created_at).toLocaleDateString()}
                </span>
              </div>
              
              <button
                onClick={() => setSelectedTimetable(timetable)}
                className="w-full btn-secondary flex items-center justify-center space-x-2"
              >
                <Eye className="h-4 w-4" />
                <span>View Schedule</span>
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Timetable;